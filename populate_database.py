from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Category, Item

engine = create_engine('postgresql:///catalog')

# Clear the existing database contents
Base.metadata.drop_all(engine)

# Create fresh tables and then populate them with sample data
Base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine)
session = DBSession()

category1 = Category(slug='soccer', name='Soccer')
session.add(category1)
session.commit()

category2 = Category(slug='basketball', name='Basketball')
session.add(category2)
session.commit()

category3 = Category(slug='baseball', name='Baseball')
session.add(category3)
session.commit()

category4 = Category(slug='frisbee', name='Frisbee')
session.add(category4)
session.commit()

category5 = Category(slug='snowboarding', name='Snowboarding')
session.add(category5)
session.commit()

category6 = Category(slug='rock-climbing', name='Rock Climbing')
session.add(category6)
session.commit()

category7 = Category(slug='foosball', name='Foosball')
session.add(category7)
session.commit()

category8 = Category(slug='skating', name='Skating')
session.add(category8)
session.commit()

category9 = Category(slug='hockey', name='Hockey')
session.add(category9)
session.commit()

item01 = Item(slug='glove', name='Glove',
              description='''
              A baseball glove or mitt is a large leather glove worn by
              baseball players of the defending team, which assists players in
              catching and fielding balls hit by a batter or thrown by a
              teammate. By convention, the glove is described by the handedness
              of the intended wearer, rather than the hand on which the glove
              is worn: a glove that fits on the left hand -— used by a
              right-handed thrower -- is called a right-handed (RH) or
              "right-hand throw" (RHT) glove. Conversely, a left-handed glove
              (LH or LHT) is worn on the right hand, allowing the player to
              throw the ball with the left hand.
              ''',
              category=category3)
session.add(item01)
session.commit()

item02 = Item(slug='climbing-rope', name='Climbing Rope',
              description='''
              Climbing ropes are typically of kernmantle construction,
              consisting of a core (kern) of long twisted fibres and an outer
              sheath (mantle) of woven coloured fibres. The core provides about
              80% of the tensile strength, while the sheath is a durable layer
              that protects the core and gives the rope desirable handling
              characteristics.
              ''',
              category=category6)
session.add(item02)
session.commit()

item03 = Item(slug='skates', name='Skates',
              description='''
              Ice skates are boots with blades attached to the bottom, used to
              propel the bearer across a sheet of ice while ice skating. The
              first ice skates were made from leg bones of horse, ox or deer,
              and were attached to feet with leather straps. These skates
              required a pole with a sharp metal spike that was used for
              pushing the skater forward, unlike modern bladed skates. Modern
              skates come in many different varieties, which are chosen
              depending on the nature of the requirements needed for the
              skating activity. They are worn recreationally in ice rinks or on
              frozen bodies of water across the globe and are used as footwear
              in many sports, including figure skating, ice hockey, bandy,
              speed skating and tour skating.
              ''',
              category=category8)
session.add(item03)
session.commit()

item04 = Item(slug='foosball-table', name='Foosball Table',
              description='''
              A vast number of different table types exist. The table brands
              used at the ITSF World Championships are Bonzini, Roberto Sport,
              Garlando, Tornado, and Leonhart. Several companies have created
              "luxury versions" of table football tables. There was a 7-metre
              table created by artist Maurizio Cattelan for a piece called
              Stadium. It takes 11 players to a side. Differences in the table
              types have great influence on the playing styles. Most tables
              have one goalie whose movements are restricted to the goal area.
              On some of these tables the goalie becomes unable to get the ball
              once it is stuck out of reach in the corner; others have sloped
              corners to return the ball to play. Another major difference
              between table types is found in the balls, which can be made of
              wood (cork in the case of traditional French tables), various
              forms of plastic or rarely even marble and metal, varying the
              speed of shots a great deal, as well as the "grip" between the
              man and the ball and the ball and the playing surface.
              ''',
              category=category7)
session.add(item04)
session.commit()

item05 = Item(slug='soccer-cleats', name='Soccer Cleats',
              description='''
              In association football, where the shoes themselves are known as
              football boots, there are three different cleat types. There are
              soft ground cleats which are made for wet weather. The soft
              ground cleats are always replaceable, and are almost always
              metal, so when they wear down they are easy to replace. There are
              firm ground cleats which are made for firm natural surfaces. In
              the UK, 'cleats' are universally known as studs. The term "studs
              up challenge" is considered a dangerous tackle made with the feet
              raised and the potentially damaging metal studs impacting on the
              legs or feet of the opponent.
              ''',
              category=category1)
session.add(item05)
session.commit()

item06 = Item(slug='jersey', name='Jersey',
              description='''
              Shirts are normally made of a polyester mesh, which does not trap
              the sweat and body heat in the same way as a shirt made of a
              natural fibre. Most professional clubs have sponsors' logos on
              the front of their shirts, which can generate significant levels
              of income, and some also offer sponsors the chance to place their
              logos on the back of their shirts. Depending on local rules,
              there may be restrictions on how large these logos may be or on
              what logos may be displayed. Competitions such as the Premier
              League may also require players to wear patches on their sleeves
              depicting the logo of the competition. A player's number is
              usually printed on the back of the shirt, although international
              teams often also place numbers on the front, and professional
              teams generally print a player's surname above his number. The
              captain of each team is usually required to wear an elasticated
              armband around the left sleeve to identify him as the captain to
              the referee and supporters.
              ''',
              category=category1)
session.add(item06)
session.commit()

item07 = Item(slug='bat', name='Bat',
              description='''
              A baseball bat is divided into several regions. The "barrel" is
              the thick part of the bat, where it is meant to hit the ball. The
              part of the barrel best for hitting the ball, according to
              construction and swinging style, is often called the "sweet
              spot". The end of the barrel is called the "top", "end" or "cap"
              of the bat. Opposite the cap, the barrel narrows until it meets
              the "handle". The handle is comparatively thin, so that batters
              can comfortably grip the bat in their hands. Sometimes,
              especially on metal bats, the handle is wrapped with a rubber or
              tape "grip". Finally, below the handle is the "knob" of the bat,
              a wider piece that keeps the bat from slipping from a batter's
              hands.
              ''',
              category=category3)
session.add(item07)
session.commit()

item08 = Item(slug='frisbee', name='Frisbee',
              description='''
              A frisbee (also called a flying disc or simply a disc) is a
              gliding toy or sporting item that is generally plastic and
              roughly 20 to 25 centimetres (8 to 10 in) in diameter with a lip,
              used recreationally and competitively for throwing and catching,
              for example, in flying disc games. The shape of the disc, an
              airfoil in cross-section, allows it to fly by generating lift as
              it moves through the air while spinning.
              ''',
              category=category4)
session.add(item08)
session.commit()

item09 = Item(slug='shinguards', name='Shinguards',
              description='''
              A shin guard or shin pad is a piece of equipment worn on the
              front of a player’s shin to protect them from injury. These are
              commonly used in sports including association football (soccer),
              baseball, ice hockey, field hockey, lacrosse, rugby, cricket, and
              other sports. This is due to either being required by the
              rules/laws of the sport or worn voluntarily by the participants
              for protective measures.
              ''',
              category=category1)
session.add(item09)
session.commit()

item10 = Item(slug='two-shinguards', name='Two Shinguards',
              description='''
              Different player positions in association football require their
              shin guards to provide different types of protection and fit.
              Defenders need the most protection. They need a heavier shin
              guard with extra ankle protection. Midfielders need protection,
              but also need to be able to move freely. Forwards need a light
              shin guard with protection and ankle support. Goalkeepers can
              wear a light shin guard with minimal protection.
              ''',
              category=category1)
session.add(item10)
session.commit()

item11 = Item(slug='snowboard', name='Snowboard',
              description='''
              Snowboards are boards that are usually the width of one's foot
              longways, with the ability to glide on snow. Snowboards are
              differentiated from monoskis by the stance of the user. In
              monoskiing, the user stands with feet inline with direction of
              travel (facing tip of monoski/downhill) (parallel to long axis of
              board), whereas in snowboarding, users stand with feet transverse
              (more or less) to the longitude of the board.
              ''',
              category=category5)
session.add(item11)
session.commit()

item12 = Item(slug='goggles', name='Goggles',
              description='''
              Goggles, or safety glasses, are forms of protective eyewear that
              usually enclose or protect the area surrounding the eye in order
              to prevent particulates, water or chemicals from striking the
              eyes. They are used in chemistry laboratories and in woodworking.
              They are often used in snow sports as well, and in swimming.
              Goggles are often worn when using power tools such as drills or
              chainsaws to prevent flying particles from damaging the eyes.
              Many types of goggles are available as prescription goggles for
              those with vision problems.
              ''',
              category=category5)
session.add(item12)
session.commit()

item13 = Item(slug='stick', name='Stick',
              description='''
              Field hockey sticks have an end which varies in shape, often
              depending on the players position. In general there are four main
              variations on head: The 'shorti' is mainly used by players
              wishing extreme control over the ball, and increase their
              maneuverability. This specific head is most associated with the
              mid-field position. (or center for Ice Hockey) The 'Midi' is used
              by players who will be hitting the ball often and need to be
              strong on their 'reverse side'. This specific head is most
              associated with the striker, or 'up-front' position. The 'Maxi'
              is similar to the 'Midi' as it has an increased surface area
              which is useful for hitting. However its strength allows it to be
              used much more effectively for stopping the ball. This head is
              used by 'defenders' and 'attackers'. The 'J Hook' again has a
              large surface area. However does not have the effectiveness of
              the 'Midi' for striking the ball, it has an increased thickness
              making it ideal for stopping the ball. This head is most commonly
              used by 'defenders'.
              ''',
              category=category9)
session.add(item13)
session.commit()
